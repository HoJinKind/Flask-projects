package Project;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.fail;

import java.util.concurrent.TimeUnit;

import org.junit.After;
import org.junit.Before;
import org.junit.Test;
import org.openqa.selenium.By;
import org.openqa.selenium.Keys;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.firefox.FirefoxDriver;

public class GenerateTest {
	 private WebDriver driver;
	 
	  private StringBuffer verificationErrors = new StringBuffer();

	  @Before
	  public void setUp() throws Exception {
	    driver = new FirefoxDriver();
	    driver.manage().timeouts().implicitlyWait(30, TimeUnit.SECONDS);
	  }

	  
	  @Test
	  public void testAccessHomePageWithLogin() throws Exception {
		  driver.get("http://127.0.0.1:5000/");
		  	String user = "tom";
			String pwd= "sutd1234";
		    driver.get("http://127.0.0.1:5000/");
		    driver.findElement(By.name("username")).click();
		    driver.findElement(By.name("username")).clear();
		    driver.findElement(By.name("username")).sendKeys(user);
		    assertEquals ("tom", user);
		    driver.findElement(By.name("pd")).clear();
		    driver.findElement(By.name("pd")).sendKeys(pwd);
		    assertEquals ("sutd1234", pwd);
		    driver.findElement(By.name("pd")).sendKeys(Keys.ENTER);
		    

			Thread.sleep(3000);
			
		    driver.get("http://127.0.0.1:5000/generate");
		    assertEquals ("generate", driver.getTitle());
		    driver.findElement(By.name("Generate1")).click();
		    
		    Thread.sleep(3000);
		    
		    assertEquals("view",driver.getTitle());
	  }
	  
	
}
	  
