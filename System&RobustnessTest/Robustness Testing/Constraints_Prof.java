package Project;

import java.util.concurrent.TimeUnit;
import org.junit.*;
import static org.junit.Assert.*;

import org.openqa.selenium.*;
import org.openqa.selenium.firefox.FirefoxDriver;
import org.openqa.selenium.support.ui.Select;



public class Constraints_Prof {
  private WebDriver driver;
  private StringBuffer verificationErrors = new StringBuffer();
  boolean result;
  @Before
  public void setUp() throws Exception {
    driver = new FirefoxDriver();
    driver.manage().timeouts().implicitlyWait(30, TimeUnit.SECONDS);
  }

  @Test
  public void Constraints_Prof_Success() throws Exception {
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
    String profName = "Sudipta";
    String dayOfWeek = "monday";
    driver.get("http://35.198.199.181:5000/constraint_Prof");
    driver.findElement(By.name("profName")).click();
    new Select(driver.findElement(By.name("profName"))).selectByVisibleText(profName);
    driver.findElement(By.name("profName")).click();
    driver.findElement(By.name("dayOfWeek")).click();
    new Select(driver.findElement(By.name("dayOfWeek"))).selectByVisibleText(dayOfWeek);
    driver.findElement(By.name("dayOfWeek")).click();
    driver.findElement(By.name("startTime")).click();
    driver.findElement(By.name("startTime")).sendKeys("08:30");
    driver.findElement(By.name("endTime")).click();
    driver.findElement(By.name("endTime")).clear();
    driver.findElement(By.name("endTime")).sendKeys("18:00");
    driver.findElement(By.xpath("(.//*[normalize-space(text()) and normalize-space(.)='End Time'])[1]/following::input[2]")).click();
  
    
    java.util.List<WebElement> links = driver.findElements(By.className("table_view_constraints2"));
    System.out.println(links.size());
    String text1;
    boolean sub_result1=false;
    boolean sub_result2=false;
    for(int i =0;i<links.size();i++) {
    	System.out.println(i + " " + links.get(i).getText());
    	text1 = links.get(i).getText();
    	if(profName.contentEquals(text1)) {
    		sub_result1=true;
    	}
    	if(dayOfWeek.contentEquals(text1)) {
    		sub_result2=true;
    	}
    	if(sub_result1==true&&sub_result2==true) {
    		result=true;
    	}
    	
    	
    }
    
    Thread.sleep(2000);
    assertEquals ("constraints_View", driver.getTitle());
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
