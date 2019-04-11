

package Project;

import java.util.concurrent.TimeUnit;
import org.junit.*;
import static org.junit.Assert.*;

import org.openqa.selenium.*;
import org.openqa.selenium.firefox.FirefoxDriver;
import org.openqa.selenium.support.ui.Select;



public class Room_Add_Failed {
  private WebDriver driver;
  private StringBuffer verificationErrors = new StringBuffer();
  boolean result;
  @Before
  public void setUp() throws Exception {
    driver = new FirefoxDriver();
    driver.manage().timeouts().implicitlyWait(30, TimeUnit.SECONDS);
  }

  @Test
  public void Room_Add_Test() throws Exception {
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
    
    Thread.sleep(3000);
    String room = "kfhle";
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
