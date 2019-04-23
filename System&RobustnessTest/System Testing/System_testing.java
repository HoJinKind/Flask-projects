package Project;

import java.util.concurrent.TimeUnit;
import org.junit.*;
import static org.junit.Assert.*;

import org.openqa.selenium.*;
import org.openqa.selenium.firefox.FirefoxDriver;
import org.openqa.selenium.support.ui.Select;



public class System_testing {
  private WebDriver driver;
  private StringBuffer verificationErrors = new StringBuffer();
  boolean result;
  @Before
  public void setUp() throws Exception {
    driver = new FirefoxDriver();
    driver.manage().timeouts().implicitlyWait(30, TimeUnit.SECONDS);
  }

  @Test
  public void Full_Test() throws Exception {
	//Login
	String user = "tom";
	String pwd= "sutd1234";
    driver.get("http://35.198.199.181:5000/");
    driver.findElement(By.name("username")).click();
    driver.findElement(By.name("username")).clear();
    driver.findElement(By.name("username")).sendKeys(user);
    assertEquals ("tom", user);
    driver.findElement(By.name("pd")).clear();
    driver.findElement(By.name("pd")).sendKeys(pwd);
    assertEquals ("sutd1234", pwd);
    driver.findElement(By.name("pd")).sendKeys(Keys.ENTER);
    
    //Add the available room information
    Thread.sleep(3000);
    String room = "2.505";
    String type = "lt";
    driver.get("http://35.198.199.181:5000/room");
    driver.findElement(By.name("roomName")).click();
    driver.findElement(By.name("roomName")).clear();
    driver.findElement(By.name("roomName")).sendKeys(room);
    new Select(driver.findElement(By.name("roomType"))).selectByVisibleText(type);
    driver.findElement(By.name("add")).click();
    java.util.List<WebElement> links = driver.findElements(By.className("table_view_room"));
    System.out.println(links.size());
    String text1;
    for(int i =0;i<links.size();i++) {
    	System.out.println(i + " " + links.get(i).getText());
    	text1 = links.get(i).getText();
    	if(room.contentEquals(text1)) {
    		result=true;
    	}
    }
    Thread.sleep(5000);
    assertTrue(result);
    assertEquals ("room", driver.getTitle());
   
    //Generate timetable (Satisfy 'Hard constraints') and View timetable generated(if generating was successful)
    driver.get("http://35.198.199.181:5000/generate");
    assertEquals ("generate", driver.getTitle());
    driver.findElement(By.name("Generate1")).click();
    Thread.sleep(3000);
    assertEquals("view",driver.getTitle());
    
    //Add Prof/Weekly constraints
    driver.get("http://35.198.199.181:5000/constraint_Prof");
    driver.findElement(By.name("profName")).click();
    new Select(driver.findElement(By.name("profName"))).selectByVisibleText("Sudipta");
    driver.findElement(By.name("profName")).click();
    driver.findElement(By.name("dayOfWeek")).click();
    new Select(driver.findElement(By.name("dayOfWeek"))).selectByVisibleText("monday");
    driver.findElement(By.name("dayOfWeek")).click();
    driver.findElement(By.name("startTime")).click();
    driver.findElement(By.name("startTime")).sendKeys("08:30");
    driver.findElement(By.name("endTime")).click();
    driver.findElement(By.name("endTime")).clear();
    driver.findElement(By.name("endTime")).sendKeys("18:00");
    driver.findElement(By.xpath("(.//*[normalize-space(text()) and normalize-space(.)='End Time'])[1]/following::input[2]")).click();
    Thread.sleep(2000);
    assertEquals ("constraints_View", driver.getTitle());
    
    //Modify timetable (Satisfy 'Hard constraints' and ¡®Prof/Weekly constraints¡¯) and View timetable generated(if modifying was successful)
    driver.get("http://35.198.199.181:5000/constraints_View");
    driver.findElement(By.linkText("Prof")).click();
    driver.findElement(By.id("generate_button_constraints")).click();
    Thread.sleep(7000);
    assertEquals ("view", driver.getTitle());
    
    //Add One Time constraints(ex. CNY)
    Thread.sleep(3000);
    driver.get("http://35.198.199.181:5000/constraint_OneTime");
    driver.findElement(By.name("eventName")).click();
    driver.findElement(By.name("eventName")).clear();
    driver.findElement(By.name("eventName")).sendKeys("CNY");
    driver.findElement(By.name("weekNo")).click();
    driver.findElement(By.name("weekNo")).clear();
    driver.findElement(By.name("weekNo")).sendKeys("5");
    driver.findElement(By.name("startTime")).click();
    driver.findElement(By.name("startTime")).clear();
    driver.findElement(By.name("startTime")).sendKeys("08:30");
    driver.findElement(By.name("endTime")).click();
    driver.findElement(By.name("endTime")).clear();
    driver.findElement(By.name("endTime")).sendKeys("18:00");
    driver.findElement(By.xpath("(.//*[normalize-space(text()) and normalize-space(.)='End Time'])[1]/following::input[2]")).click();
    Thread.sleep(2000);
    assertEquals ("constraints_View", driver.getTitle());
    
    //Modify timetable (Satisfy ¡®Hard constraints¡¯ and ¡®Soft constraints¡¯) and View timetable generated(if modifying was successful)
    driver.get("http://35.198.199.181:5000/constraints_View");
    driver.findElement(By.xpath("(.//*[normalize-space(text()) and normalize-space(.)='monday'])[1]/following::input[2]")).click();
    Thread.sleep(2000);
    assertEquals ("view", driver.getTitle());
    
    //Logout
    driver.findElement(By.xpath("(.//*[normalize-space(text()) and normalize-space(.)='View'])[1]/following::button[1]")).click(); 
    driver.switchTo().alert().accept();
    Thread.sleep(5000);
    assertEquals ("login", driver.getTitle());
    
  }

  @After
  public void tearDown() throws Exception {
    driver.quit();
    String verificationErrorString = verificationErrors.toString();
    if (!"".equals(verificationErrorString)) {
      fail(verificationErrorString);
    }
  }

}
